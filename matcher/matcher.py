from pathlib import Path

import cv2
import torch
import numpy as np

from matcher.model_loader import ModelLoader
from matcher.preprocess import (
    read_image,
    preprocess,
)
from matcher.schemas import MatchResult


class GIMMatcher:

    def __init__(
        self,
        loader: ModelLoader,
    ):

        self.loader = loader
        self.device = loader.device
        self.detector = loader.detector
        self.matcher = loader.matcher

    def match(
        self,
        query_path: str,
        candidate_path: str,
    ) -> MatchResult:

        query_image = read_image(query_path, grayscale=True)
        candidate_image = read_image(candidate_path,grayscale=True)
        
        query_image, scale_query_image = preprocess(query_image,grayscale=True)
        candidate_image, scale_candidate_image = preprocess(candidate_image,grayscale=True)

        query_image = query_image.to(self.device)[None]
        candidate_image = candidate_image.to(self.device)[None]
        scale_candidate_image = scale_candidate_image.to(self.device)[None]
        scale_query_image = scale_query_image.to(self.device)[None]

        data = dict(color0=query_image, color1=candidate_image, image0=query_image, image1=candidate_image)
        data.update(dict(gray0=query_image, gray1=candidate_image))

        size0 = torch.tensor(data["gray0"].shape[-2:][::-1])[None]
        size1 = torch.tensor(data["gray1"].shape[-2:][::-1])[None]

        data.update(dict(size0=size0, size1=size1))
        data.update(dict(scale0=scale_query_image, scale1=scale_candidate_image))

        pred = {}
        with torch.no_grad():
            pred.update({k + '0': v for k, v in self.detector({
                "image": data["gray0"],
            }).items()})
            pred.update({k + '1': v for k, v in self.detector({
                "image": data["gray1"],
            }).items()})
            pred.update(self.matcher({**pred, **data,
                               **{'image_size0': data['size0'],
                                  'image_size1': data['size1']}}))
        
        kpts0 = torch.cat([kp * s for kp, s in zip(pred['keypoints0'], data['scale0'][:, None])])
        kpts1 = torch.cat([kp * s for kp, s in zip(pred['keypoints1'], data['scale1'][:, None])])
        m_bids = torch.nonzero(pred['keypoints0'].sum(dim=2) > -1)[:, 0]
        matches = pred['matches']
        bs = data['image0'].size(0)
        kpts0 = torch.cat([kpts0[m_bids == b_id][matches[b_id][..., 0]] for b_id in range(bs)])
        kpts1 = torch.cat([kpts1[m_bids == b_id][matches[b_id][..., 1]] for b_id in range(bs)])
        b_ids = torch.cat([m_bids[m_bids == b_id][matches[b_id][..., 0]] for b_id in range(bs)])
        mconf = torch.cat(pred['scores'])

        try:
        # robust fitting
            _, mask = cv2.findFundamentalMat(kpts0.cpu().detach().numpy(),
                                        kpts1.cpu().detach().numpy(),
                                        cv2.USAC_MAGSAC, ransacReprojThreshold=1.0,
                                        confidence=0.999999, maxIters=10000)
            mask = mask.ravel() > 0

            score = np.mean(mconf[mask].cpu().detach().numpy())
            num_matches = mconf.shape[0]
            num_inliers = np.sum(mask)
        
        except cv2.error as e:
            #print(f"Error in cv2.findFundamentalMat: {e}")
            print("Skipping this pair due to insufficient matches.")
            score = 0
            num_matches = 0
            num_inliers = 0

        

        return MatchResult(
            query_path=query_path,
            score=score,
            num_matches=num_matches,
            num_inliers=num_inliers,
        )



