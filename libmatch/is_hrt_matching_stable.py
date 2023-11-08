def check_hrt_matching(hrt_match, residents, hospitals):
    '''
    Checks whether a matching of the hospital resident matching problem with ties is stable or not

    Args:
        hrt_match (dict): A hashmap containing hospital names (str) as the key and a list of residents' names (str) as a value
        residents (list): A list of residents (objects of the 'Student' class)
        hospitals (list): A list of hospitals (objects of the 'Course' class)

    Returns:
        boolean
    '''
    #hrt match except Student/Course objects instead of strings
    modified_hrt_match = {}
    for hospital in hrt_match:
        hospital_object = find_object(hospital, hospitals)
        modified_hrt_match[hospital_object] = []
        for resident in hrt_match[hospital]:
            resident_object = find_object(resident, residents)
            modified_hrt_match[hospital_object].append(resident_object)


    unmatched_residents = [ resident for resident in residents ]

    #   Check hospitals didn't go over capacity
    for hospital in modified_hrt_match:
        num_residents = len(modified_hrt_match[hospital])
        if num_residents > hospital.capacity:
            print()
            print('INSTABILITY: {} is over capacity. # Residents = {}, Capacity = {}'.format(hospital.name, num_residents, hospital.capacity))
            print()
            return False

    #   Check blocking pairs where matched resident strictly prefers another hospital 
    #   and that hospital either has space or strictly prefers them to another resident 
    for hospital in modified_hrt_match:
        for resident in modified_hrt_match[hospital]:
            hospital_rank = resident.weights[hospital]
            resident_strict_list = strict_preferences(hospital_rank, resident.weights)
            for prefered_hospital in resident_strict_list:
                number_of_residents = len(modified_hrt_match[prefered_hospital])
                
                # prefered hospital has space
                if number_of_residents < prefered_hospital.capacity:
                    print()
                    print('INSTABILITY: {} is under capacity ({}/{}) and {} prefers it over current match {}'.format(prefered_hospital.name, number_of_residents, prefered_hospital.capacity, resident.name, hospital.name))
                    print('{} preference list: {}'.format(resident.name, resident.weights))
                    print()
                    return False
                
                # resident prefers other hospital and that hospital prefers that resident.
                blocking_pair = strict_mutual_preference(resident, prefered_hospital, modified_hrt_match)
                if blocking_pair[0]:
                    print()
                    print('INSTABILITY: {} prefers {} over current match {} and {} prefers {} over current match {}'.format(resident.name, prefered_hospital.name, hospital.name, prefered_hospital.name, resident.name, blocking_pair[1].name))
                    print('{} preference list: {}'.format(resident.name, resident.weights))
                    print('{} preference list: {}'.format(prefered_hospital.name, prefered_hospital.weights))
                    print()
                    return False
            
            unmatched_residents.remove(resident)      
            
    #   Check blocking pairs where there is unmatched resident with list of preferences
    #   and a hospital in that list either has space or strictly prefers them to another resident 
    #   (won't do anything if all residents were matched)
    for resident in unmatched_residents:
        for hospital in resident.weights.keys():
            number_of_residents = len(modified_hrt_match[hospital])
            if number_of_residents < hospital.capacity:
                print()
                print('INSTABILITY: {} is under capacity ({}/{}) and {} (unmatched) has it in preference list'.format(hospital.name, number_of_residents, hospital.capacity, resident.name))
                print()
                return False 

            blocking_pair = strict_mutual_preference(resident, hospital, modified_hrt_match)
            if blocking_pair[0]:
                print()
                print('INSTABILITY: {} (unmatched) prefers {} and {} prefers {} over current match {}'.format(resident.name, hospital.name, hospital.name, prefered_hospital.name, resident.name, blocking_pair[1].name))
                print('{} preference list: {}'.format(resident.name, resident.weights))
                print('{} preference list: {}'.format(hospital.name, hospital.weights))
                print()
                return False

    return True

def find_object(name, hospitals):
    for hospital in hospitals:
        if hospital.name == name:
            return hospital

def strict_preferences(rank, rankings):
    '''
    Helper function for check_matching()

    Args:
        rank (int): given weight of a hospital/resident
        rankings (dict): A hashmap containing hospital/resident names (str) as the key and an integer as a value
    
    Returns:
        A list of hospitals/residents that a resident/hospital strictly prefers over its currently matched hospital/resident
    '''
    prefered_list = []
    for other, weight in rankings.items():
        if weight > rank:
            prefered_list.append(other)
    return prefered_list


def strict_mutual_preference(resident, hospital, modified_hrt_match):
    '''
    Helper function for check_matching()

    Args:
        resident (Student object): A resident that has preferences to switch into another hospital
        hospital (Course object): A hospital that resident would like to switch into
        num_of_residents (int): An integer representing the number of residents currently matched to hospital
    Returns:
        A boolean representing whether resident and hospital are a blocking pair
    '''
    asking_resident_weight = hospital.weights[resident]
    hospitals_current_residents = modified_hrt_match[hospital]
    for matched_resident in hospitals_current_residents:
        matched_resident_weight = hospital.weights[matched_resident]
        if asking_resident_weight > matched_resident_weight:
            return True, matched_resident
    return False, None

