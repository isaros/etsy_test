#### utils functions ####

# Save every the elements of a list a new file
def save_in_file(file_name,data):
    with open(file_name, 'w') as f:
        for line in data :
            f.write(line+'\n')
