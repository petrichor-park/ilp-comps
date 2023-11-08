def galeShapley(man_preferences, woman_preferences):
    single_men = list(man_preferences.keys())
    single_women = list(woman_preferences.keys())
    married_women = {}

    while single_men:
        man = single_men.pop(0)
        for woman in man_preferences[man]:
            if woman in single_women:
                married_women[woman] = man
                single_women.remove(woman)
                break
            elif sheWantsHimAnyway(man, married_women[woman], woman_preferences[woman]):
                single_men.append(married_women[woman])
                married_women[woman] = man
                break
                    
    return [(husband, wife) for wife, husband in married_women.items()]
    

def sheWantsHimAnyway(suitor, husband, woman_likey_list):
    for dude in woman_likey_list:
        if dude == suitor:
            return True
        if dude == husband:
            return False
        

if __name__ == "__main__":
    man_preferences = {"1": ["1", "3", "2"], 
                       "2": ["2", "3", "1"], 
                       "3": ["2", "3", "1"]}
    woman_preferences = {"1": ["3", "2", "1"], 
                         "2": ["2", "3", "1"], 
                         "3": ["2", "3", "1"]}
    #correct matching: [('1', '1'), ('2', '2'), ('3', '3')]
    csprofs = {'Eric': ['Claudio','Sunrose','Deanna','Kate'],
               'Sneha': ['Claudio', 'Deanna', 'Kate', 'Sunrose'],
                'Layla': ['Kate', 'Deanna', 'Claudio', 'Sunrose'],
                'Kiran': ['Sunrose', 'Deanna', 'Kate', 'Claudio']}
    mathprofs = {'Claudio': ['Sneha', 'Eric', 'Layla', 'Kiran'],
                 'Deanna': ['Kiran', 'Layla', 'Eric', 'Sneha'],
                 'Kate': ['Sneha', 'Layla', 'Kiran', 'Eric'],
                 'Sunrose': ['Layla', 'Eric', 'Kiran', 'Sneha']}
    #correct matching: [('Claudio', 'Sneha'), ('Kate', 'Layla'), ('Sunrose', 'Eric'), ('Deanna', 'Kiran')]
    print(galeShapley(csprofs, mathprofs))