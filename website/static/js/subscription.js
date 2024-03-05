let selectedCard = null;

function selectPlan(subs_type, price) {
    if (selectedCard) {
        selectedCard.style.border = '1px solid #ccc';
    }
    selectedCard = document.getElementById(subs_type);
    selectedCard.style.border = '2px solid blue';
    document.getElementById('subs_type').value = subs_type;
    document.getElementById('price').value = price;
}

function checkIfFormIsNull(event) {

    const subs_type = document.getElementById('subs_type').value;
    const price = document.getElementById('price').value;

    if (subs_type == '' | price == '') {
        alert('Please select a card before subscribing.');
        event.preventDefault();
    }

}


