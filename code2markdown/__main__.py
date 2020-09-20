
from pathlib import Path
from code2markdown import Code


def main():
	output_dir = Path.cwd()
	code = Code.Code()
	code.dump(output_dir=output_dir)
	
	
if __name__ == "__main__":
	main()
