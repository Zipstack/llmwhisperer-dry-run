# LLMWhisperer Dry Run
Run LLMWhisperer on sample files to check suitability for your projects

## Supported operating systems
You should be able to run this on Linux or on a Mac. Windows is not supported.

## Keys you'll need
You'll need an API key for [LLMWhisperer](https://unstract.com/llmwhisperer/), which you can get for free. Once you have the key, please add it to the `.env` file in the root of the project. A sample `.env` file is provided in the repo for you to copy.

## Running the code
Clone this repo and change to the `llmwhisperer-dry-run` directory. We suggest you run the code after you've created a Python virtual environment. You can create a virtual environment by running the following command:

```bash
python3 -m venv .venv
```

Next, activate the virtual environment:

```bash
source .venv/bin/activate
```

Now, install the dependencies:

```bash
pip install -r requirements.txt
```

Next, copy the `sample.env` file to `.env`, edit the `.env` file to add your and LLMWhisperer key:

```bash
cp sample.env .env
```

Finally, run the code:

```bash
python main.py <path to PDF file or directory with PDFs>
```
## Limitations
- Although the LLMWhisperer service supports many different file types like common office document formats, images, PDFs, etc, the code currently only supports PDF files. If you have other file types, you'll need to convert them to PDF before running the code.
- Currently, only Linux and Mac are supported. Windows is not supported.
- In the code, the extraction mode is hardcoded to "text". If you want to extract from scanned documents or images where text is not selectable, you'll need to change the code and set EXTRACTION_MODE to "ocr". Please see the [LLMWhisperer API documentation](https://docs.unstract.com/llm_whisperer/apis/llm_whisperer_text_extraction_api) for more information.
