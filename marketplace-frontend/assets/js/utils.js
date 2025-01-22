const utils = {
    formatPrice(price) {
        return `$${parseFloat(price).toFixed(2)}`;
    },

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString();
    },

    showAlert(message, type = 'error') {
        alert(message); // You can replace this with a better alert system
    }
};