def mini(releve, date):
    if not releve or len(releve) != len(date):
        return None
    min_temperature = releve[0]
    min_annee = date[0]
    for temperature, annee in zip(releve, date):
        if temperature < min_temperature:
            min_temperature = temperature
            min_annee = annee
    return min_temperature, min_annee


t_moy = [14.9, 13.3, 13.1, 12.5, 13.0, 13.6, 13.7]
annees = [2013, 2014, 2015, 2016, 2017, 2018, 2019]

# print(mini(t_moy, annees))


def inverse_chaine(chaine):
    result = ""
    for caractere in chaine:
        result = caractere + result
    return result


def est_palindrome(chaine):
    inverse = inverse_chaine(chaine)
    return inverse == chaine


def est_nbre_palindrome(nbre):
    chaine = str(nbre)
    return est_palindrome(chaine)


print(est_nbre_palindrome(214312))
print(est_nbre_palindrome(213312))
