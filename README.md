# Flashcards
As falas irão aparecer depois do tempo apresentado em cada botão de nível de dificuldade, ex: `Hard (15 seg)` significa que a frase atual irá aparecer depois de 15 segundos. Ou seja, ele responde - única e exclusivamente - ao horário.

Os tempos estão pré-definidos em `language/views_common.py` através da variável `time_step` - os construtores seguem a sua [documentação](https://docs.python.org/2/library/datetime.html#datetime.timedelta). Enquanto que os saltos temporais são descritos por `std_step` e por `extr_step`, onde o primeiro indica qual intervalo de tempo será considerado de forma padrão, enquanto que o segundo corresponde à condição extra: marcar como fácil para algo visto pela primeira vez.

Dessa forma, têm-se as regras sobre as escolhas da dificuldade.

**Regras da Dificuldade**

 - ***Easy:*** sendo a primeira aparição, o próximo tempo será o `extr_stp`-nésimo elemento do `time_step`, caso contrário será o próximo tempo cadastrado. Controle implementado em `language/views_common/get_easy_step`;
 - ***Medium:*** sendo a primeira aparição, o próximo tempo será o `2 * std_step`-nésimo elemento do `time_step`, caso contrário será o tempo já sinalizado. Controle implementado em `language/views_common/get_medium_step`;
 - ***Hard:*** o próximo tempo será o tempo anterior cadastrado, exceto quando for primeiro: permanecerá nesse. Controle implementado em `language/views_common/get_hard_step`.
