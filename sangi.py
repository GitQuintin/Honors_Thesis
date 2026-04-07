
import numpy as np
from sympy import symbols, sturm, count_roots, solve


class equation_system():

    def __init__(self):

        found_root = False
        setup = True
        self.root_detected = False

        while found_root == False:

            self.roots = []

            while setup:
                print("---------------------------------------------------------------------------------------------------------------------------------------------------------- \n"
                "Welcome to the Sangi Root Finder! \n"
                "This program will help you find integer roots of polynomials using a method similar to synthetic division. Let's get started! \n"
                "----------------------------------------------------------------------------------------------------------------------------------------------------------")
                print("Enter the coefficients of the equation, starting with the highest degree, separated by spaces. Use a dash before a number to indicate it is negative.")
                coefficients = input().split()
                coefficients = [int(x) for x in coefficients] # Convert input to integers

                print("Coefficients entered:", coefficients)

                interval = True
                while interval:
                    print("What range would you like to search for roots in? Enter the lower and upper bounds separated by a space.")
                    bounds = input().split()
                    self.lower_bound = int(bounds[0])
                    self.upper_bound = int(bounds[1])

                    self.sturm = self.sangi_sturm(coefficients)

                    if self.sturm == 0:
                        print("No roots found in the specified range. Please try again with different bounds.")
                        continue # Try a new interval if no roots are found
            
                    print("Would you like to try a new range? (Y/N)")
                    response = input().upper()
                    if response == "Y":
                        continue # Restart the process to enter new bounds
                    elif response == "N":
                        interval = False
                        continue
                
                print("Proceed with provided polynomial and range? (Y/N)")
                response = input().upper()
                if response == "Y":
                    setup = False
                elif response == "N":
                    continue
            

            max_root = 0 # Longest root
            self.max_coefficient = 0 # Longest coefficient
            for coef in coefficients:
                if len(str(abs(self.max_coefficient))) < len(str(abs(coef))):
                    self.max_coefficient = len(str(abs(coef)))
            
            for root in self.roots:
                if len(str(abs(max_root))) < len(str(abs(root))):
                    max_root = len(str(abs(root)))
                    
            self.rows = len(coefficients) + 1 # Add one for the ANS row
            self.columns = self.max_coefficient + 1

            self.matrix = self.formatting(coefficients, True)
            
            self.matrix_copy = self.matrix # Make a copy of the original matrix to reset to after each guess
            self.coefficients_copy = coefficients# Make a copy of the original coefficients to reset to after each guess
            self.first_pass = True
            self.first_shift = True
            self.shifts = 0
    

            print(self)

            process = True
            found_root = False # Initialize as False

            while process:
                print("How many digits do you think the root has?")
                self.shift_amount = int(input())
                self.columns = self.max_coefficient + ((self.shift_amount-1)*(self.rows-1)) # Update columns based on the shift amount for formatting the matrix correctly after shifts
                if self.columns < 5: self.columns = 5 # Set a minimum column width for better display, can be adjusted as needed
                self.matrix = self.formatting(self.coefficients, False) # Reformat the matrix with the new column width based on the shift amount
                
                for i in range(self.shift_amount):
                    self.shift()
                    self.pass_through()
                    self.reverse_shift()
                    
                    if self.root_detected:
                        found_root = True
                        process = False
                        break # Exit the for loop
                
                if found_root:
                    print("Root successfully detected!")
                else:
                    print("The guessed root was incorrect.")
                    print("Would you like to try again with a different guess? (Y/N)")
                    response = input().upper()
                    if response == "Y":
                            self.matrix = self.matrix_copy # Reset the matrix to the original state for the next iteration if needed
                            self.coefficients = self.coefficients_copy + [0] # Reset the coefficients to the original state for the next iteration if needed
                            self.first_pass = True
                            self.shifts = 0
                            continue # Restart the process to guess again
                    elif response == "N":
                        process = False # Stop the while loop if the user does not want to guess again
                        found_root = True # Set to True to exit the outer while loop


            #     # After the for loop finishes, stop the while loop
            #     process = False

            # # Final feedback outside the loop
            # if found_root:
            #     print("Root successfully detected!")
            # else:
            #     print("The guessed root was incorrect.")
            #     process = False # Ensure the loop is stopped if the root was not found
            #     found_root = True # Reset for the next iteration if needed




    def __str__(self):

        out = ""
        # Use the actual length of the current matrix
        for row in self.matrix:
            out += "| "
            for cell in row:
                # {0:<8} aligns text to the left with 8 spaces for a cleaner look than \t
                out += "{0:<8}".format(str(cell)) 
            out += "|\n"
        return out
    
    def display(self):

        out = ""
        # Use the actual length of the current matrix
        for row in self.matrix:
            out += "| "
            for cell in row:
                # {0:<8} aligns text to the left with 8 spaces for a cleaner look than \t
                out += "{0:<8}".format(str(cell)) 
            out += "|\n"
        return out
    
    def shift(self):
        self.shifts += 1

        if self.first_shift:
            # print("How many digits do you think the root has?")
            # self.shift_amount = int(input())
            degree = len(self.coefficients) - 1
            self.first_shift = False
        else:
            degree = (len(self.coefficients)-2)  # Subtract one more to account for the ANS row that is not shifted  
        
        #shifter = 10 ** (shift_amount-1)
        #degrees = self.rows - 2
        # Shift the coefficients to the right increasingly to the specified amount, filling in zeros as needed
        shifted_matrix = []
        for i in range(len(self.matrix)-1, -1, -1):
            shift = (self.shift_amount-self.shifts)*(degree)
            if degree < 0:
                shifted_matrix.append(self.matrix[i])
                continue #ANS row is not shifted
            shifted_row = np.roll(self.matrix[i], -shift) # Might change for guess with more than two digits
            shifted_matrix.append(shifted_row.tolist())
            degree -= 1
        
        # Reverse the matrix to maintain original row order
        shifted_matrix.reverse()
        self.matrix = shifted_matrix

        print(self)

        return self.matrix
    
    def reverse_shift(self):

        #degrees = self.rows - 1 
        degree = len(self.coefficients) - 2
        # Shift the coefficients to the left increasingly to the specified amount, filling in zeros as needed
        shifted_matrix = []
        for i in range(len(self.matrix)-1, -1, -1):
            shift = (self.shift_amount-self.shifts)*(degree)
            if degree < 0:
                shifted_matrix.append(self.matrix[i])
                continue #ANS row is not shifted
            # Shifting back the same amount as before but in the opposite direction to reverse the shift
            shifted_row = np.roll(self.matrix[i], shift) # Might change for guess with more than two digits
            shifted_matrix.append(shifted_row.tolist())
            degree -= 1
        
        # Reverse the matrix to maintain original row order
        shifted_matrix.reverse()
        self.matrix = shifted_matrix
        
        print(self)

        return self.matrix
    
    def pass_through(self):
        #Reverse the matrix to match the order of coefficients with the place values, starting with the highest
        self.matrix.reverse()

        # Prompt the user for their guess of the next digit in the root, starting with the highest digit on the first pass
        if self.first_pass:
            print("What is the value of the highest digit in the root?")
            guess = int(input())
            self.guess = guess
            self.first_guess = guess * (10 ** (self.shift_amount-1)) # Convert the first guess to its actual value based on the shift amount
            self.first_pass = False
        else:
            print("What is the value of the next digit in the root?")
            guess = int(input())
            self.guess = guess
            self.first_guess += guess * (10 ** (self.shift_amount-self.shifts)) # Add the next guess to the total value of the root based on the shift amount
            
        calc_matrix = [0] * (self.rows-1) + [self.first_guess]  # Initialize a new matrix to store the calculations, starting with all zeros

        # Create a new matrix to use the numbers the rows represent for the calculations
        for row in range(self.rows-1):
            for col in range(self.columns):
                # Calculate the power of 10 based on the column's place value
                power = self.columns - 1 - col
                calc_matrix[row] += self.matrix[row][col] * (10 ** power)

        # Multiply each row by guess and add it to next one above it, starting from the bottom
        # Then repeat but stopping one row earlier, until reach the bottom row
        for i in range(self.rows-2):
            for row in range(self.rows):
                if row == self.rows - (2+i): break #ANS row is not multiplied, and stop one row earlier each time
                calc_matrix[row+1] += calc_matrix[row] * guess

                print(calc_matrix)

            # Stop if row is zerod out, since then we found a root
            if calc_matrix[-2] == 0: 
                #Print the root
                print(f"You found a root: {calc_matrix[-1]}")
                self.root_detected = True
                break
            print("\n")

        # Seperate the digits like before to get the new matrix
        self.matrix = self.formatting(calc_matrix, False)
        print(self)

        return self.matrix
    
    def formatting(self, coefficients, is_initial=True):
        #first row of zeros (ANS row)
        if is_initial:
            table = "0" * (self.columns)
            strMatrix = ["0" * self.columns]
        else:
            table = ""
            strMatrix = []
            
        intMatrix = []
        is_negative = False
        # Convert everything to a single string of digits
        # This joins [10, 2, 3] into "1023". Including the padding for the matrix and the dashes for negative numbers
        for i in range(len(coefficients)-1, -1, -1):

            if coefficients[i] < 0:
                strMatrix.append("0" * (self.columns - (len(str(abs(coefficients[i]))))) + "-" + "-".join(str(abs(coefficients[i]))))
            else:
                strMatrix.append("0" * (self.columns - (len(str(coefficients[i])))) + str(coefficients[i]))

            # if coefficients[i] < 0:
            #     coefficients[i] = abs(coefficients[i])
            #     #Start negative, rest are attached with join
            #     if coefficients[i] < 10:
            #         table += "0" * (self.columns-1) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-1) + "-" + "-".join(str(coefficients[i])))
            #     elif coefficients[i] < 100:
            #         table += "0" * (self.columns-2) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-2) + "-" + "-".join(str(coefficients[i])))
            #     elif coefficients[i] < 1000:
            #         table += "0" * (self.columns-3) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-3) + "-" + "-".join(str(coefficients[i])))
            #     elif coefficients[i] < 10000:
            #         table += "0" * (self.columns-4) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-4) + "-" + "-".join(str(coefficients[i])))
            #     elif coefficients[i] < 100000:
            #         table += "0" * (self.columns-5) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-5) + "-" + "-".join(str(coefficients[i])))
            #     elif coefficients[i] < 1000000:
            #         table += "0" * (self.columns-6) + "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("0" * (self.columns-6) + "-" + "-".join(str(coefficients[i])))
            #     else:
            #         table += "-" + "-".join(str(coefficients[i]))
            #         strMatrix.append("-" + "-".join(str(coefficients[i])))
            #     continue
            # if abs(coefficients[i]) < 10:
            #     table += "0" * (self.columns-1) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-1) + str(coefficients[i]))
            # elif abs(coefficients[i]) < 100:
            #     table += "0" * (self.columns-2) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-2) + str(coefficients[i]))
            # elif abs(coefficients[i]) < 1000:
            #     table += "0" * (self.columns-3) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-3) + str(coefficients[i]))
            # elif abs(coefficients[i]) < 10000:
            #     table += "0" * (self.columns-4) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-4) + str(coefficients[i]))
            # elif abs(coefficients[i]) < 100000:
            #     table += "0" * (self.columns-5) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-5) + str(coefficients[i]))
            # elif abs(coefficients[i]) < 1000000:
            #     table += "0" * (self.columns-6) + str(coefficients[i])
            #     strMatrix.append("0" * (self.columns-6) + str(coefficients[i]))
            # else:
            #     table += str(coefficients[i])
            #     strMatrix.append(str(coefficients[i]))

        intMatrix = []

        for row in strMatrix:
            new_row = []
            is_negative = False
            
            for char in row:
                if char == "-":
                    is_negative = True
                    continue
                
                # Convert to int and apply sign
                value = int(char)
                if is_negative:
                    value = -value
                    is_negative = False
                    
                new_row.append(value)
            
            intMatrix.append(new_row)

        self.matrix = intMatrix
        self.coefficients = coefficients
        
        return self.matrix 
    
    def sangi_sturm(self, coefficients):
        # Compute Sturm sequence using SymPy

        x = symbols('x')
        p = "" # Convert the coefficients back into a polynomial expression
        for i in range(len(coefficients)):
            power = len(coefficients) - 1 - i
            coeff = coefficients[i]
            if coeff != 0:
                p += f"{coeff}*x**{power} + "
        p = p[:-3] # Remove the trailing " + "

        self.roots = solve(p, x)
        print(f"Polynomial: {p}")
        num_roots = count_roots(p, self.lower_bound, self.upper_bound) # Count the number of roots in the interval [lower_bound, upper_bound]
        if num_roots == 0:
            print(f"There are no roots in the interval [{self.lower_bound}, {self.upper_bound}]")
        else:
            print(f"There are {num_roots} roots in the interval [{self.lower_bound}, {self.upper_bound}]")

        return num_roots
