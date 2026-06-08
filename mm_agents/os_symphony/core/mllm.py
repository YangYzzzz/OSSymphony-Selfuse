import base64
import json
import re

import numpy as np

from mm_agents.os_symphony.core.engine import (
    LMMEngineAnthropic,
    LMMEngineAzureOpenAI,
    LMMEngineHuggingFace,
    LMMEngineOpenAI,
    LMMEngineOpenRouter,
    LMMEngineParasail,
    LMMEnginevLLM,
    LMMEngineGemini,
)


class LMMAgent:
    def __init__(self, engine_params: dict, system_prompt=None, engine=None):
        if engine is None:
            if engine_params is not None:
                engine_type = engine_params.get("engine_type")
                if engine_type == "openai":
                    self.engine = LMMEngineOpenAI(**engine_params)
                elif engine_type == "anthropic":
                    self.engine = LMMEngineAnthropic(**engine_params)
                elif engine_type == "azure":
                    self.engine = LMMEngineAzureOpenAI(**engine_params)
                elif engine_type == "vllm":
                    self.engine = LMMEnginevLLM(**engine_params)
                elif engine_type == "huggingface":
                    self.engine = LMMEngineHuggingFace(**engine_params)
                elif engine_type == "gemini":
                    self.engine = LMMEngineGemini(**engine_params)
                elif engine_type == "open_router":
                    self.engine = LMMEngineOpenRouter(**engine_params)
                elif engine_type == "parasail":
                    self.engine = LMMEngineParasail(**engine_params)
                else:
                    raise ValueError(f"engine_type '{engine_type}' is not supported")
            else:
                raise ValueError("engine_params must be provided")
        else:
            self.engine = engine

        self.messages = []  # Empty messages
        self.agent_name = engine_params.get("agent_name")
        if system_prompt:
            self.add_system_prompt(system_prompt)
        else:
            self.add_system_prompt("You are a helpful assistant.")

    def encode_image(self, image_content):
        # if image_content is a path to an image file, check type of the image_content to verify
        if isinstance(image_content, str):
            with open(image_content, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        else:
            return base64.b64encode(image_content).decode("utf-8")

    def reset(
        self,
    ):

        self.messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": self.system_prompt}],
            }
        ]

    def add_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt
        if len(self.messages) > 0:
            self.messages[0] = {
                "role": "system",
                "content": [{"type": "text", "text": self.system_prompt}],
            }
        else:
            self.messages.append(
                {
                    "role": "system",
                    "content": [{"type": "text", "text": self.system_prompt}],
                }
            )

    def remove_message_at(self, index):
        """Remove a message at a given index"""
        if index < len(self.messages):
            self.messages.pop(index)

    def replace_message_at(
        self, index, text_content, image_content=None, image_detail="high"
    ):
        """Replace a message at a given index"""
        if index < len(self.messages):
            self.messages[index] = {
                "role": self.messages[index]["role"],
                "content": [{"type": "text", "text": text_content}],
            }
            if image_content:
                base64_image = self.encode_image(image_content)
                self.messages[index]["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": image_detail,
                        },
                    }
                )

    def add_message(
        self,
        text_content,
        image_content=None,
        role=None,
        image_detail="high",
        put_text_last=True,
    ):
        """Add a new message to the list of messages"""

        # API-style inference from OpenAI and AzureOpenAI
        if isinstance(
            self.engine,
            (
                LMMEngineOpenAI,
                LMMEngineAzureOpenAI,
                LMMEngineHuggingFace,
                LMMEngineGemini,
                LMMEngineOpenRouter,
                LMMEngineParasail,
            ),
        ):
            # infer role from previous message
            if role != "user":
                if self.messages[-1]["role"] == "system":
                    role = "user"
                elif self.messages[-1]["role"] == "user":
                    role = "assistant"
                elif self.messages[-1]["role"] == "assistant":
                    role = "user"

            message = {
                "role": role,
                "content": [{"type": "text", "text": text_content}],
            }

            if isinstance(image_content, np.ndarray) or image_content:
                # Check if image_content is a list or a single image
                if isinstance(image_content, list):
                    # If image_content is a list of images, loop through each image
                    for image in image_content:
                        base64_image = self.encode_image(image)
                        message["content"].append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": image_detail,
                                },
                            }
                        )
                else:
                    # If image_content is a single image, handle it directly
                    base64_image = self.encode_image(image_content)
                    message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": image_detail,
                            },
                        }
                    )

            # Rotate text to be the last message if desired
            if put_text_last:
                text_content = message["content"].pop(0)
                message["content"].append(text_content)

            self.messages.append(message)

        # For API-style inference from Anthropic
        elif isinstance(self.engine, LMMEngineAnthropic):
            # infer role from previous message
            if role != "user":
                if self.messages[-1]["role"] == "system":
                    role = "user"
                elif self.messages[-1]["role"] == "user":
                    role = "assistant"
                elif self.messages[-1]["role"] == "assistant":
                    role = "user"

            message = {
                "role": role,
                "content": [{"type": "text", "text": text_content}],
            }

            if image_content:
                # Check if image_content is a list or a single image
                if isinstance(image_content, list):
                    # If image_content is a list of images, loop through each image
                    for image in image_content:
                        base64_image = self.encode_image(image)
                        message["content"].append(
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image,
                                },
                            }
                        )
                else:
                    # If image_content is a single image, handle it directly
                    base64_image = self.encode_image(image_content)
                    message["content"].append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image,
                            },
                        }
                    )
            self.messages.append(message)

        # Locally hosted vLLM model inference
        elif isinstance(self.engine, LMMEnginevLLM):
            # infer role from previous message
            if role != "user":
                if self.messages[-1]["role"] == "system":
                    role = "user"
                elif self.messages[-1]["role"] == "user":
                    role = "assistant"
                elif self.messages[-1]["role"] == "assistant":
                    role = "user"

            message = {
                "role": role,
                "content": [{"type": "text", "text": text_content}],
            }

            if image_content:
                # Check if image_content is a list or a single image
                if isinstance(image_content, list):
                    # If image_content is a list of images, loop through each image
                    for image in image_content:
                        base64_image = self.encode_image(image)
                        message["content"].append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image;base64,{base64_image}"
                                },
                            }
                        )
                else:
                    # If image_content is a single image, handle it directly
                    base64_image = self.encode_image(image_content)
                    message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image;base64,{base64_image}"},
                        }
                    )
                    
                if put_text_last:
                    text_content = message["content"].pop(0)
                    message["content"].append(text_content)
            self.messages.append(message)
        else:
            raise ValueError("engine_type is not supported")

    def get_response(
        self,
        user_message=None,
        messages=None,
        temperature=0.0,
        max_new_tokens=32168,
        use_thinking=False,
        **kwargs,
    ):
        """Generate the next response based on previous messages"""
        if messages is None:
            messages = self.messages
        if user_message:
            messages.append(
                {"role": "user", "content": [{"type": "text", "text": user_message}]}
            )

        # Regular generation
        # if use_thinking:
        #     return self.engine.generate_with_thinking(
        #         messages,
        #         temperature=temperature,
        #         max_new_tokens=max_new_tokens,
        #         **kwargs,
        #     )

        return self.engine.generate(
            messages,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            **kwargs,
        )

    def get_json_response(self, *args, **kwargs):
        response = self.get_response(*args, **kwargs)
        self.last_usage = None
        if isinstance(response, tuple):
            response, self.last_usage = response
        raw_response = str(response or "")
        return raw_response, self._load_json_response(raw_response)

    def _load_json_response(self, raw_response):
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError as original_error:
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_response, re.DOTALL | re.IGNORECASE)
            if match:
                return json.loads(match.group(1).strip())
            extracted = self._extract_embedded_json(raw_response)
            if extracted is not None:
                return extracted
            raise original_error

    def _extract_embedded_json(self, raw_response):
        decoder = json.JSONDecoder()
        for idx, char in enumerate(raw_response):
            if char not in "[{":
                continue
            try:
                data, _ = decoder.raw_decode(raw_response[idx:])
                return data
            except json.JSONDecodeError:
                continue
        return None
