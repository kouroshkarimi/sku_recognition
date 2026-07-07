from os.path import join

import torch


from local_matcher.networks.lightglue.superpoint import SuperPoint
from local_matcher.networks.lightglue.models.matchers.lightglue import LightGlue


class ModelLoader:

    def __init__(
        self,
        model_name: str = "gim_lightglue",
        device: str = None,
    ):

        self.model_name = model_name

        self.device = (
            device
            if device is not None
            else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        self.detector = None
        self.matcher = None

        self.load()

    def load(self):

        if self.model_name == "gim_lightglue":

            ckpt = "gim_lightglue_100h.ckpt"

            self.detector = SuperPoint(
                {
                    "max_num_keypoints": 2048,
                    "force_num_keypoints": True,
                    "detection_threshold": 0.0,
                    "nms_radius": 3,
                    "trainable": False,
                }
            )

            self.matcher = LightGlue(
                {
                    "filter_threshold": 0.1,
                    "flash": False,
                    "checkpointed": True,
                }
            )

            checkpoint = join(
                "weights",
                ckpt,
            )

            state_dict = torch.load(
                checkpoint,
                map_location="cpu",
            )

            if "state_dict" in state_dict:
                state_dict = state_dict["state_dict"]

            detector_state = {}

            for key, value in state_dict.items():

                if key.startswith("superpoint."):

                    detector_state[
                        key.replace(
                            "superpoint.",
                            "",
                        )
                    ] = value

            self.detector.load_state_dict(
                detector_state,
            )

            matcher_state = {}

            for key, value in state_dict.items():

                if key.startswith("model."):

                    matcher_state[
                        key.replace(
                            "model.",
                            "",
                        )
                    ] = value

            self.matcher.load_state_dict(
                matcher_state,
            )

            self.detector.eval().to(self.device)

            self.matcher.eval().to(self.device)

        else:
            raise ValueError(
                f"Unsupported model: {self.model_name}"
            )