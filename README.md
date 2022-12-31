# GradeAnalyzer
Compute statistics for [Genesis Grade Portal](https://parents.ewrsd.k12.nj.us/genesis/parents?gohome=true).


## Usage
1. Save the HTML of a specific Genesis class
    - URL format should follow `https://parents.ewrsd.k12.nj.us/genesis/parents?tab1=studentdata&tab2=gradebook&tab3...`
2. Run `main.py` to parse and extract existing grades and values
3. Input the filename of the saved HTML file
    - `"economics.html"` is provided as an example to run this program
4. Use `Target Grade slider` to set the desired final grade, will be used to predict needed assignment weight to achieve this. 
5. Use `Next Weight slider` to predict the _grade_ needed on the next assignment to end with desired final grade
    - _Note: `Next Weight slider` depends on the grade set with `Target Grade slider`_
    
    
