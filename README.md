# house_price_prediction

Dataset: 

https://drive.google.com/file/d/1t_XXs6MBk2lk94XB1ozX2UiwkXzswrql/view?usp=sharing 

Inference script: 

`house_pricing_API.py`


Input example:

```
[{ 
    'bathrooms': 2, 
    'floor': 0.5, 
    'rooms': 3, 
    'surface': 78, 
    'state': 'nou', 
    'zone': 'Buna Ziua'
},
{
    'bathrooms': 2, 
    'floor': 0.5, 
    'rooms': 3, 
    'surface': 78, 
    'state': 'nou', 
    'zone': 'Marasti'
}]
```
* floor in [0,1] - the value is normalized with the max number of building floors, e.g.: 1/4 (floor 1 of 4)

