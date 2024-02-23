from .module1 import MyClass, utility_function

def main():
	obj = MyClass("Alice")
	print(obj.greet())
	print("Utility function output:", utility_function(10))

if __name__ == "__main__":
	main()
