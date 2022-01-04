"""This module is used for connecting to and creating the database for pySign"""

try:
    import curses
except ImportError:
    print("Curses failed to import.")

import logging
from os import path
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from getpass import getpass

base = declarative_base()

def authenticate() -> tuple[str, str]:
  """Authenticates a user through a call to fetch_creds.

  Returns:
    Email and password from fetch_creds

  """

  return fetch_creds(curses.initscr())


def fetch_creds(stdscr) -> tuple[str, str]:
  """Fetches user credentials.

  Note:
    Makes use of the curses package for console interaction.

  Args:
    stdscr: Window object representing the entire screen.

  Returns:
    Email address and password.

  """

  logging.info("Authenticating user...")

  # Clear the window and allow echoing
  stdscr.clear()
  curses.echo()

  email = ""
  pw = ""

  # Prompt the user for their email address and password
  stdscr.addstr(0, 0, "=== Authenticate yourself ===")
  stdscr.addstr(1, 0, "Email: ")

  try:
    stdscr(email = "utf-8").decode().getstr()
  except ValueError:
    logging.critical("Failed to retrieve email address; defaulting to none.")

  try:
    pw = getpass("Password: ", None)
  except ValueError:
    logging.critical("Failed to retrieve password; defaulting to none.")

  return (email, pw)


class User(base):
  """Creates a user table using SQLAlchemy.

  Note:
    Not required if user does not wish to have access
    to extra fields or mature signs and some word lists.

  Args:
    user_email (str): SigningSavvy email address.
    user_pass (str): SigningSavvy password.

  Attributes:
    user_email (str): SigningSavvy email address.
    user_pass (str): SigningSavvy password.

  """

  __tablename__ = "user"

  user_id = Column(Integer, primary_key=True)
  user_email = Column(String, nullable=False)
  user_pass = Column(String, nullable=False)


  def __init__(self, user_email, user_pass):
    self.user_email = user_email
    self.user_pass = user_pass


class URI(base):
  """Creates an location table using SQLAlchemy.

  Notes:
    Contains the uniform resource identifier for the content.

  Args:
    location_name (str): Location name.
    location_uri (str): Remote URI for the location.

  Attributes:
    location_name (str): Location name.
    location_uri (str): Remote URI for the location.

  """

  __tablename__ = "uri"

  location_id = Column(Integer, primary_key=True)
  location_name = Column(String)
  location_uri = Column(String)


  def __init__(self, location_name, location_uri):
    self.location_name = location_name
    self.location_uri = location_uri


class Word(base):
  """Creates a word table using SQLAlchemy.

  Args:
    word_id (number): ID used in remote URI.
    synoynm_id (number): ID for synonyms.
    word_name (str): Word name.
    word_definition (str): Word definition.
    word_usage (str): Example of word use.

  Attributes:
    word_id (number): ID used in remote URI.
    synoynm_id (number): ID for synonyms.
    word_name (str): Word name.
    word_definition (str): Word definition.
    word_usage (str): Example of word use.

  """

  __tablename__ = "word"

  word_id = Column(Integer, primary_key=True)
  synoynm_id = Column(Integer, nullable=False)
  word_name = Column(String, nullable=False)
  word_definition = Column(String, nullable=False)
  word_usage = Column(String)


  def __init__(self, word_id, synonym_id, name, definition, usage):
    self.word_id = word_id
    self.synonym_id = synonym_id
    self.name = name
    self.definition = definition
    self.usage = usage


class Variant(base):
  """Creates a variant table using SQLAlchemy.

  Args:
    variant_uri (str): Remote URI for word variant.
    variant_vidld (str): Remote URI for 360p video.
    variant_vidsd (str): Remote URI for 540p video.
    variant_vidhd (str): Remote URI for 720p video.
    variant_index (number): Index used in remote URI.
    variant_type (str): Sign type.
    variant_desc (str): Variant description.
    variant_tip (str): Combined mnemonic and notice.
    word_id (number): Reference to the word.

  Attributes:
    variant_uri (str): Remote URI for word variant.
    variant_vidld (str): Remote URI for 360p video.
    variant_vidsd (str): Remote URI for 540p video.
    variant_vidhd (str): Remote URI for 720p video.
    variant_index (number): Index used in remote URI.
    variant_type (str): Sign type.
    variant_desc (str): Variant description.
    variant_tip (str): Combined mnemonic and notice.
    word_id (number): Reference to the word.

  """

  __tablename__ = "variant"

  variant_id = Column(Integer, primary_key=True)
  variant_uri = Column(String, nullable=False)
  variant_vidld = Column(String, nullable=False)
  variant_vidsd = Column(String, nullable=False)
  variant_vidhd = Column(String, nullable=False)
  variant_index = Column(Integer, nullable=False)
  variant_type = Column(String)
  variant_desc = Column(String)
  variant_tip = Column(String)
  word_id = Column(Integer, ForeignKey("word.word_id"))


  def __init__(self, variant_uri, variant_vidld, variant_vidsd, variant_vidhd,
    variant_index, variant_type, variant_desc, variant_tip, word_id):
    self.variant_uri = variant_uri
    self.variant_vidld = variant_vidld
    self.variant_vidsd = variant_vidsd
    self.variant_vidhd = variant_vidhd
    self.variant_index = variant_index
    self.variant_type = variant_type
    self.variant_desc = variant_desc
    self.variant_tip = variant_tip
    self.word_id = word_id


class WordList(base):
  """Creates a word list table using SQLAlchemy.

  Args:
    word_list_name (str): Name of the word_list.
    word_id (number): Reference to the word.

  Attributes:
    word_list_name (str): Name of the word_list.
    word_id (number): Reference to the word.

  """

  __tablename__ = "wordlist"

  word_list_id = Column(Integer, primary_key=True)
  word_list_name = Column(String)
  word_id = Column(Integer, ForeignKey("word.word_id"))


  def __init__(self, word_list_name, word_id):
    self.word_list_name = word_list_name
    self.word_id = word_id


class Sentence(base):
  """Creates a sentence table using SQLAlchemy.

  Args:
    sentence (str): Sentence.
    description (str): Description of the sentence.

  Attributes:
    sentence (str): Sentence.
    description (str): Description of the sentence.

  """

  __tablename__ = "sentence"

  sentence_id = Column(Integer, primary_key=True)
  sentence = Column(String)
  description = Column(String)


  def __init__(self, sentence, description):
    self.sentence = sentence
    self.description = description


class SentenceList(base):
  """Creates a sentence list table using SQLAlchemy.

  Args:
    sentence_list_name (str): Name of the sentence list.
    sentence_id (number): Reference to the sentence.

  Attributes:
    wordlist_name (str): Name of the wordlist.
    word_id (number): Reference to the word.

  """

  __tablename__ = "sentencelist"

  sentence_list_id = Column(Integer, primary_key=True)
  sentence_list_name = Column(String)
  sentence_id = Column(Integer, ForeignKey("sentence.sentence_id"))


  def __init__(self, sentence_list_name, sentence_id):
    self.sentence_list_name = sentence_list_name
    self.sentence_id = sentence_id


class SentenceGlossary(base):
  """Creates a sentence glossary table using SQLAlchemy.

  Args:
    sentence_id (number): Reference to a sentence.
    word_id (number): Reference to a word.

  Attributes:
    sentence_id (number): Reference to a sentence.
    word_id (number): Reference to a word.

  """

  __tablename__ = "sentenceglossary"

  sentence_id = Column(Integer, ForeignKey("sentence.sentence_id"))
  word_id = Column(Integer, ForeignKey("word.word_id"))


  def __init__(self, sentence_id, word_id):
    self.sentence_id = sentence_id
    self.word_id = word_id


class Article(base):
  """Creates an article table using SQLAlchemy.

  Args:
    article_id (number): ID used in remote URI.
    author_name (str): Full name of article author.
    date (str): Article date.
    html (str): Full HTML content for article.

  Attributes:
    article_id (number): ID used in remote URI.
    author_name (str): Full name of article author.
    date (str): Article date.
    html (str): Full HTML content for article.

  """

  __tablename__ = "article"

  article_id = Column(Integer, primary_key=True)
  author_name = Column(String)
  date = Column(String)
  html = Column(String, nullable=False)


  def __init__(self, article_id, author_name, date, html):
    self.article_id = article_id
    self.author_name = author_name
    self.date = date
    self.html = html


def connect():
  """Initiate a connection to the SQLite database with SQLAlchemy.

  Returns:
    SQLAlchemy database engine linked to the db file or null.

  """

  logging.info("Connecting to database...")

  # Absolute path hack to get SQLAlchemy to create the engine
  p = path.abspath("../db/pysign.db3")
  engine = create_engine(f"sqlite:///{p}", future=True)

  return engine


def create_session(engine) -> Session:
  """Creates a database for use with `pysign`.

  Returns:
    engine: database engine

  """

  logging.info("Connecting to database...")

  base.metadata.create_all(engine)
  session = Session(engine)

  return session

def create_all(session: Session) -> None:
  """Uses a Session to create all of the data needed to fill the database.

  """
