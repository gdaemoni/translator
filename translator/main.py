from googletrans import Translator
from googletrans.constants import LANGUAGES
from argparse import ArgumentParser
from pprint import pprint
from pathlib import Path
import sys
import os


SAVE_FILE = Path.cwd() / 'save_file'
DEFAULT_FILE = Path.cwd() / 'AnkiCards'


def translate_sentences(sentences: list, sentrnces_tr: list) -> list:
	res = []
	for i, sentrnce_tr in enumerate(sentrnces_tr):
		if sentrnce_tr.extra_data is not None:
			passible_tr = sentrnce_tr.extra_data['possible-translations']
			if passible_tr is not None:
				print('\t\t', sentences[i].strip())
				for item in passible_tr[0][2]:
					res.append(item[0])
					print('\t\t', item[0].upper())
				if i + 1 < len(sentrnces_tr):
					print('\t\t\t-----')
		else:
			print("No translations found")
	return res


def make_AnkiCards(word: str, translate: dict) -> list:
	cards = []
	number_card = 0

	for part_of_speech, translations in translate.items():
		translation_variants = f'{part_of_speech} <br><br> - '
		examples = '<br><br> Примеры <br><br> '
		display_line = f'\t\t {word.upper()}: \t - '

		for val in translations:
			if type(val).__name__ == str.__name__:
				translation_variants += val + ' - '
				display_line += val.upper() + ' - '
			else:
				for example in val:
					if type(example).__name__ == str.__name__:
						examples += '<br>' + example
		presign = ''.join(' ' for i in range(100 - len(display_line)))
		print(number_card, display_line, f'{presign}{part_of_speech}')
		number_card += 1
		card = f"{part_of_speech} <br><br> {word} | {translation_variants} | {examples} \n"
		cards.append(card)
	return cards


def add_path_save(path: str):
	if os.path.isdir(path):
		print('Is a directory: ', path)
		exit(1)
	with open(SAVE_FILE, 'w') as f:
		f.write(path)


def get_path_to_save() -> str:
	if not os.path.exists(SAVE_FILE):
		add_path_save('')
	with open(SAVE_FILE, 'r') as f:
		path = f.read()
		if not len(path):
			path = DEFAULT_FILE
		return path


def write_to_file(cards: list):
	indexes = input("What to save?")
	if indexes is not None:
		with open(get_path_to_save(), 'a') as f:
			for number in indexes:
				f.write(cards[int(number)])


def arg() -> {}:
	parser = ArgumentParser()
	parser.add_argument("-s", "--non-save",
	                    action='store_false',
	                    default=True,
	                    help="disables saving the current transfer in anki cards")
	parser.add_argument("-l", "--language",
	                    type=str,
	                    default='ru',
	                    help="ru, eng, fr show all languages -a")
	parser.add_argument('-a', '--all-language',
	                    action="store_true",
	                    help="show all languages")
	parser.add_argument('words',
	                    nargs='+',
	                    type=str,)
	parser.add_argument('-f', '--file',
						action='store_true',
						help='file in which the anki cards are saved ')
	parser.add_argument('-e', '--examples-number',
						help="number of examples, default 3",
						type=int,
						default=3)

	args = parser.parse_args()
	if args.all_language:
		pprint(LANGUAGES)
		exit(1)
	elif args.file:
		add_path_save(args.words[0])
		exit(1)
	return args.words, args.examples_number, args.language, args.non_save


def translation_word(word: str, exn: int, save: str, translation_information):
	parts_of_speech = {}
	if translation_information.extra_data['all-translations'] is not None:
		for translation_options in translation_information.extra_data['all-translations']:
			part_of_speech = translation_options[0]
			translations = translation_options[1][0:exn]
			parts_of_speech[part_of_speech] = translations
		if translation_information.extra_data['definitions'] is not None:
			for definitions_options in translation_information.extra_data['definitions']:
				definitions = definitions_options[1][0:3]
				part_of_speech_def = definitions_options[0]
				if part_of_speech_def in parts_of_speech.keys():
					s = parts_of_speech[part_of_speech_def]
					defin = []
					for definition in definitions:
						defin.append(definition[-1])
					s.append(defin)
					parts_of_speech[part_of_speech_def] = s
		cards = make_AnkiCards(word, parts_of_speech)
		if save:
			write_to_file(cards)

	else:
		print('No translations found')


def main():
	words, examples_number, dest, save = arg()
	translator = Translator()
	pre_translator = ' '.join(words).split('.')
	translation_information = translator.translate(pre_translator, dest=dest)
	if len(words) > 1:
		translate_sentences(pre_translator, translation_information)
	else:
		translation_word(pre_translator[0], examples_number, save, translation_information[0])


if __name__ == '__main__':
	main()
