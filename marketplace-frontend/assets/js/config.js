const config = {
    API_URL: 'http://localhost:8000/api',
    BASE_URL: 'http://localhost:8000',
    getImageUrl: function(imagePath) {
        // Remove any leading slashes to avoid double slashes
        const cleanPath = imagePath.replace(/^\//, '');
        return `${this.BASE_URL}/${cleanPath}`;
    }
};