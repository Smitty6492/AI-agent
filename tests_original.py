from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def run_tests():
    print("Result for current directory:")
    #print(get_files_info("calculator", "."))
    #print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    
    #("\nResult for 'pkg' directory:")
    #print(get_files_info("calculator", "pkg"))

    #print("\nResult for '/bin' directory:")
    #print(get_files_info("calculator", "/bin"))

    #print("\nResult for '../' directory:")
    #print(get_files_info("calculator", "../"))
    
    ("\nResult for 'pkg' directory:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    
    ("\nResult for 'pkg' directory:")
    print(get_file_content("calculator", "bin/cat"))
    

if __name__ == "__main__":
    run_tests()
