__author__ = 'Jorge Haddad'


def test_bouncy(char_list, index=1, ordem_anterior=None):
    if index == len(char_list):
        return False

    if char_list[index] > char_list[index - 1]:
        nova_ordem = '>'
    elif char_list[index] < char_list[index - 1]:
        nova_ordem = '<'
    else:
        nova_ordem = ordem_anterior

    if (nova_ordem == '<' and ordem_anterior == '>') or (nova_ordem == '>' and ordem_anterior == '<'):
        return True

    return test_bouncy(char_list, index + 1, nova_ordem)


def count_bouncys(proportion_threshold):
    current_number = 100
    bouncy_count = 0

    while True:

        if test_bouncy(list(str(current_number))):
            bouncy_count += 1

        if bouncy_count / current_number >= proportion_threshold:
            return current_number
        current_number += 1

print(count_bouncys(0.99))
