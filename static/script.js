const inputFields = document.querySelectorAll('input');
        inputFields.forEach(input => {
            input.addEventListener('focus', () => {
                const helpTextId = `${input.id}Help`;
                const helpText = document.getElementById(helpTextId);
                helpText.classList.add('active');
            });
            input.addEventListener('blur', () => {
                const helpTextId = `${input.id}Help`;
                const helpText = document.getElementById(helpTextId);
                helpText.classList.remove('active');
            });
        });