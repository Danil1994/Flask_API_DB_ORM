def made_list_with_dicts(_list: list) -> list[dict]:
    answer = []
    for el in _list:
        _dict = {'Group name': el.name, 'Group id': el.id}
        answer.append(_dict)
    return answer


def made_list_with_students_dict(students_list):
    answer = []
    for stud in students_list:
        _dict = {f'Student {stud.id}': {'first name ': stud.first_name, 'last_name': stud.last_name}}
        # _dict={str(stud)}
        answer.append(_dict)
    return answer
