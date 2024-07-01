import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { MealCard } from '../components/MealCard';
import { mealPlan } from '../data/meal_plan';
import { formatDate } from '../utils/formatDate';
import { UpdateListsFromMealPlanModal } from '../components/UpdateListsFromMealPlanModal';


export function MealPlan() {
    const [alertShow, setAlertShow] = useState<boolean>(false);
    const creationDateObject = new Date(mealPlan.creation_date);
    const creationDate = formatDate(creationDateObject);

    const endDateObject = new Date(mealPlan.creation_date);
    endDateObject.setDate(endDateObject.getDate() + 7);
    const endDate = formatDate(endDateObject);

    return (
        <Container className="pb-4">
            <div className="page_title mt-3">
                MealPlan {`for ${creationDate} to ${endDate}`}
            </div>
            <div className="d-flex justify-content-center mt-2 mb-5 gap-4">
                <Button
                    className="custom_button"
                >
                    {'Make New Plan'}
                </Button>
                <Button
                    className="custom_button"
                    onClick={() => setAlertShow(true)}
                >
                    {'Update Pantry & Shopping List'}
                </Button>
                <UpdateListsFromMealPlanModal
                    show={alertShow}
                    onHide={() => setAlertShow(false)}
                />
            </div>
            <div>
                {Object.keys(mealPlan.meals).map((day: string) => (
                    <div key={day} className="mb-3">
                        <MealCard
                            day={Number(day)}
                            meal={mealPlan.meals[Number(day)]}
                        />
                    </div>
                ))}
            </div>
        </Container>
    )
}
