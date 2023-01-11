const likeBtns = document.querySelectorAll('.likeBtn');

likeBtns.forEach(button => {
    button.addEventListener('click', likeToggle)
});

function likeToggle() {
    let liked;
    this.classList.contains('fa-solid') ? liked = true : liked = false;
    let likeCount = this.innerText;

    if (liked === true) {
        fetch(`/unlike/${this.id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.classList.remove('fa-solid');
                this.classList.add('fa-regular');
                likeCount--;
                this.innerText = ` ${likeCount}`;
            })

    } else {
        fetch(`/like/${this.id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.classList.remove('fa-regular');
                this.classList.add('fa-solid');
                likeCount++;
                this.innerText = ` ${likeCount}`;
            })
    }
}

