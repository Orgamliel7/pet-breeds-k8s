import dataclasses
import sys
import ast

def determine_pet_type(data): # Based on specific key words unique to each API response
    if 'breed_group' in data or 'bred_for' in data:
        return 'Dog'
    elif 'vcahospitals_url' in data or 'cfa_url' in data:
        return 'Cat'
    else:
        return 'Unknown'

DOG_ASCII = """
,-.___,-.
\_/_ _\_/
  )O_O(
 { (_) }
  `-^-'  
"""

CAT_ASCII = """
 /\_/\\
( o.o )
 > ^ <
"""

def main():
    count = 1
    dog_count = 0
    cat_count = 0
    
    for line in sys.stdin:
        if "Received:" in line:
            try:
                dict_str = line[line.index('{'):].strip() # JSON-like string from line
                data = ast.literal_eval(dict_str) # convert string to Python object
                breed_name = data.get('name', 'Unknown Breed') #default breed_name = Unknown Breed (if not found)
                pet_type = determine_pet_type(data)
                print(f"{count}. {pet_type} - {breed_name}")
                
                if pet_type == 'Dog':
                    print(DOG_ASCII)
                    dog_count += 1
                elif pet_type == 'Cat':
                    print(CAT_ASCII)
                    cat_count += 1
                
                print()  # blank line for separation
                count += 1
            except Exception as e:
                print(f"Error processing line: {e}")
    
    print("Summary:")
    print(f"Dogs: {dog_count}")
    print(f"Cats: {cat_count}")

if __name__ == "__main__":
    main()