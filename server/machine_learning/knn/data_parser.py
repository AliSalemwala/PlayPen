f = open('malware_files_data.dms', 'r').read().split('\n')[:-1]

ids = [i for i in range(0, len(f))]

tupled_hash = list(zip(ids, f))

file_to_id_hash = dict(tupled_hash)

print(file_to_id_hash)