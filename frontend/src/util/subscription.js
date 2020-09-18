const categories = [
    {value: 20, text: '-20', year: 2000},
    {value: 18, text: '-18', year: 2002},
    {value: 16, text: '-16', year: 2004},
    {value: 14, text: '-14', year: 2006},
    {value: 12, text: '-12', year: 2008},
    {value: 10, text: '-10', year: 2010},
    {value: 8, text: '-8', year: 2012},
]
  
function normalcategory(gender, birthyear){
    // return the normal category for a player based on gender and birthyear
    console.log('normalcat', birthyear)
    let g = gender == 'M' ? 'B' : 'G';
    let age = 99;
    categories.forEach(function(c){
        if (c.year <= birthyear) age = c.value
    })
    return g + age;
}

function catselect(birthyear) {
    let cats = [];
    categories.forEach(function(c){
        if (c.year <= birthyear) cats.push(c)
    })
    console.log('catselect', birthyear, cats)
    return cats
}

export {categories, normalcategory, catselect};