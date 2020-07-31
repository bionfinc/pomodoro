function getPlantImage(plantNumber, plantStage) {
    switch (plantStage) {
        case 1:
            let image1 = document.getElementById("plant-image" + plantNumber);
            image1.classList.remove('plant7');
            image1.classList.add('plant1');
            image1.src = '/static/images/tomato-plant/seed-1.png';
            return;
        case 2:
            let image2 = document.getElementById("plant-image" + plantNumber);
            image2.classList.remove('plant1');
            image2.classList.add('plant2');
            image2.src = '/static/images/tomato-plant/plant-2.png';
            return;
        case 3:
            let image3 = document.getElementById("plant-image" + plantNumber);
            image3.classList.remove('plant2');
            image3.classList.add('plant3');
            image3.src = '/static/images/tomato-plant/plant-3.png';
            return;
        case 4:
            let image4 = document.getElementById("plant-image" + plantNumber);
            image4.classList.remove('plant3');
            image4.classList.add('plant4');
            image4.src = '/static/images/tomato-plant/plant-4.png';
            return;
        case 5:
            let image5 = document.getElementById("plant-image" + plantNumber);
            image5.classList.remove('plant4');
            image5.classList.add('plant5');
            image5.src = '/static/images/tomato-plant/plant-5.png';
            return;
        case 6:
            let image6 = document.getElementById("plant-image" + plantNumber);
            image6.classList.remove('plant5');
            image6.classList.add('plant6');
            image6.src = '/static/images/tomato-plant/plant-6.png';
            return;
        case 7:
            let image7 = document.getElementById("plant-image" + plantNumber);
            image7.classList.remove('plant6');
            image7.classList.add('plant7');
            image7.src = '/static/images/tomato-plant/plant-7.png';
            return;
        default:
            break;
    }
}

function generateButtonText(plantNumber, plantStage) {
    let button = document.getElementById("plant-button" + plantNumber);
    button.style.margin = '10px';

    switch (plantStage) {
        case 1:
            button.innerHTML = "Plant a seed <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 2:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 3:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 4:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 5:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 6:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        case 7:
            button.innerHTML = "Water the plant <br> (Costs " + getUpgradeCost(plantStage) + " points)";
            return;
        default:
            break;
    }
}

function getUpgradeCost(plantStage) {
    switch (plantStage) {
        case 1:
            return 8;
        case 2:
            return 10;
        case 3:
            return 10;
        case 4:
            return 10;
        case 5:
            return 10;
        case 6:
            return 10;
        case 7:
            return 10;
        default:
            break;
    }
}

function getAwardImage(award_type, award_number) {
    switch (award_type) {
        case 0:
            let image0 = document.getElementById("award-image" + award_number)
            image0.style.maxWidth = '150px';
            image0.style.maxHeight = '150px';
            image0.classList.add('mx-auto');
            image0.classList.add('mt-auto');
            image0.src = '../static/images/food-rewards/empty-plate.png';
            return;
        case 1:
            let image1 = document.getElementById("award-image" + award_number)
            image1.style.maxWidth = '150px';
            image1.style.maxHeight = '150px';
            image1.classList.add('mx-auto');
            image1.classList.add('mt-auto');
            image1.src = '/static/images/food-rewards/1-tomato-basil-spaghetti.png';
            return;
        case 2:
            let image2 = document.getElementById("award-image" + award_number)
            image2.style.maxWidth = '150px';
            image2.style.maxHeight = '150px';
            image2.classList.add('mx-auto');
            image2.classList.add('mt-auto');
            image2.src = '/static/images/food-rewards/2-tomato-lasagna.png';
            return;
        case 3:
            let image3 = document.getElementById("award-image" + award_number)
            image3.style.maxWidth = '150px';
            image3.style.maxHeight = '150px';
            image3.classList.add('mx-auto');
            image3.classList.add('mt-auto');
            image3.src = '/static/images/food-rewards/3-tomato-pizza.png';
            return;
        case 4:
            let image4 = document.getElementById("award-image" + award_number)
            image4.style.maxWidth = '150px';
            image4.style.maxHeight = '150px';
            image4.classList.add('mx-auto');
            image4.classList.add('mt-auto');
            image4.src = '/static/images/food-rewards/4-tomato-sauce-penne.png';
            return;
        case 5:
            let image5 = document.getElementById("award-image" + award_number)
            image5.style.maxWidth = '150px';
            image5.style.maxHeight = '150px';
            image5.classList.add('mx-auto');
            image5.classList.add('mt-auto');
            image5.src = '/static/images/food-rewards/5-tomato-sauce-spaghetti.png';
            return;
    }
}

function updateProfileInformationScore(newScore) {
    document.getElementById("profile-score").innerText = "Score: " + newScore
}