// A simple JavaScript sample with various constructs for visualization

function calculateTotal(items) {
    let total = 0;

    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.price > 0) {
            total += item.price * (item.quantity || 1);
        }
    }

    return total;
}

// Example data
const inventory = [
    { id: 1, name: 'Widget', price: 9.99, quantity: 5 },
    { id: 2, name: 'Gadget', price: 19.99, quantity: 2 },
    { id: 3, name: 'Sample', price: 0, quantity: 10 }
];

// Calculate and output the total
const total = calculateTotal(inventory);
console.log(`Total: $${total.toFixed(2)}`);

// Conditional logic
if (total > 50) {
    console.log('Bulk discount applied!');
} else {
    console.log('Regular pricing');
} 