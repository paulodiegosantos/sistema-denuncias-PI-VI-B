import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from dotenv import load_dotenv

# Localiza a raiz do projeto e carrega o arquivo .env.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def get_fernet():
    key = os.environ.get('FERNET_KEY')

    if not key:
        raise ImproperlyConfigured(
            'A variável FERNET_KEY não foi configurada. '
            'Execute configurar.bat.'
        )

    try:
        return Fernet(key.encode())
    except (ValueError, TypeError):
        raise ImproperlyConfigured(
            'A chave FERNET_KEY configurada é inválida.'
        )


class EncryptedTextField(models.TextField):

    def get_prep_value(self, value):
        value = super().get_prep_value(value)

        if value is None or value == '':
            return value

        return get_fernet().encrypt(
            value.encode()
        ).decode()

    def from_db_value(self, value, expression, connection):
        if value is None or value == '':
            return value

        try:
            return get_fernet().decrypt(
                value.encode()
            ).decode()
        except InvalidToken:
            raise ValueError(
                'Não foi possível descriptografar o dado. '
                'Verifique se a chave Fernet corresponde ao banco.'
            )