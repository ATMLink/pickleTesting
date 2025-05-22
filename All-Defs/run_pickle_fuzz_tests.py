import pickle
from generate_random_object import generate_random_object

def run_pickle_fuzz_tests(num_tests=100, max_depth=4, output_prefix="data"):
    with open(f"{output_prefix}.in", "w", encoding="utf-8") as infile, \
         open(f"{output_prefix}.out", "w", encoding="utf-8") as outfile:
        
        for i in range(num_tests):
            obj = generate_random_object(max_depth=max_depth)
            infile.write(f"#{i}: {repr(obj)}\\n")
            try:
                pickled = pickle.dumps(obj, protocol=4)
                unpickled = pickle.loads(pickled)
                outfile.write(f"#{i}: success\\n")
            except Exception as e:
                outfile.write(f"#{i}: error: {str(e)}\\n")

if __name__ == "__main__":
    run_pickle_fuzz_tests()