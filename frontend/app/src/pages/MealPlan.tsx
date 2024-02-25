import { Button } from 'react-bootstrap';
import { mealPlan } from '../data/meal_plan';


export function MealPlan() {
    const creationDate = mealPlan.creation_date;

    return (
        <>
            <div className="page_title mt-3">
                MealPlan {`for ${creationDate}`}
            </div>
            <div className="d-flex justify-content-center mt-2 mb-5 gap-4">
                <Button
                    className="custom_button"
                >
                    Make New Plan
                </Button>
            </div>
        </>
    )
}
