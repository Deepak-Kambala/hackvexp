def factorial(n):
    """Calculate factorial of a number"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def main():
    num = 5
    print(f"The factorial of {num} is {factorial(num)}")

if __name__ == "__main__":
    main()