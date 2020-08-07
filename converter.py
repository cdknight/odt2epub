import pypandoc
import sys
import re
import tempfile
import os
from colorama import init
from termcolor import colored
import yaml

init()

def md_to_epub(odt_md):
    print(colored("stage 2: ", "blue") + "create temp dir for unpacking split mdfiles")


    with tempfile.TemporaryDirectory() as tmpdirname:
        print(colored("stage 3: ", "blue") + "split mdfiles by specified regex")
        separators = re.split(re.compile(config['chapter_regex_string']), odt_md)[1:]
        render_md = ""

        print(colored("stage 4: ", "blue") + "modify and output mdfiles for pandoc processing")
        for i, separate in enumerate(separators):
            print(colored("\texport: ", "yellow") + f"processing chapter {i+1} for final epub export")
            separate = re.sub(r"^\*\*$", '', separate, flags=re.MULTILINE) # Clean up annoying double-asterisks that get rendered because of messy markdown
            separate = f"# Chapter {i+1}\n\n" + separate + "\n\n"
            render_md += separate



        print(colored("stage 5: ", "blue") + "prepare metadata")
        yaml_s = "---\n" + yaml.dump(config['metadata']) + "\n---\n" # Use the dashes for adding metadata at the "beginning."

        render_md += yaml_s

        print(colored("stage 6: ", "blue") + "convert document to epub")
        extra_args = []
        if config.get('toc'):
            extra_args.append('--toc')
        if config.get('css'):
            extra_args.append(f"--css={config.get('css')}")

        pypandoc.convert_text(render_md, 'epub', format="md", outputfile=output_epub, extra_args=extra_args)
        print(colored("Exported", "green") + f" {input_odt} to {output_epub}. Enjoy!")

   


def odt_to_md(file):
    print(colored("stage 1: ", "blue") + "convert odt to md via html")
    return pypandoc.convert_text(
        pypandoc.convert_file(input_odt, 'html'),
        'md', format="html"
        )


try:
    input_odt = sys.argv[1]
    output_epub = sys.argv[2]
except IndexError:
    exit("Please provide valid input and output documents as the first and second arguments, respectively.\nUsage: convert.py [infile.odt] [outfile.epub]")

try:
    with open("config.yaml") as yamlf:
        config = yaml.safe_load(yamlf)
except Exception:
    exit("Could not read config file!")


if __name__ == "__main__":
    odt_md = odt_to_md(input_odt)
    md_to_epub(odt_md)
