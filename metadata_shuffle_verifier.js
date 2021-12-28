const crypto = require('crypto');

let array = []
for( let i = 1; i <= 8880; i++)
{
    array.push(i);
}

let random_index = 0;
for( let i = 8880-1; i > 0; i--)
{
    let byte_input = Buffer.from(String(random_index), 'utf8');
    let hash_object = crypto.createHash('sha256').update(byte_input);
    let hash_val = hash_object.digest('hex');
    let hash_result = BigInt('0x' + hash_val);
    random_index = hash_result % BigInt(i+1);

    let temp = array[i];
    array[i] = array[random_index];
    array[random_index] = temp;
}

console.log(array);