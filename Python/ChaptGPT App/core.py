import openai

class Predictor:
    def __init__(self, api_key_file: str):
        # Read the API key from the specified file
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
        
        # Set the API key
        openai.api_key = api_key
        
        # Set the model to use (in this case, ChatGPT)
        self.model_engine = "text-davinci-002"
    
    def predict(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7, top_p: float = 1, frequency_penalty: float = 0, presence_penalty: float = 0) -> str:
        # Use the openai library to generate a response
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        return completion.choices[0].text
    
    
# Create a Predictor instance
predictor = Predictor("TOKEN.txt")

# Call the predict() method to get a response to a question
response = predictor.predict("What is the capital of France?")
print(response)
