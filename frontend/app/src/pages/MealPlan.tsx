import { useState } from 'react';
import { Button, Container, Modal } from 'react-bootstrap';
import { MealCard } from '../components/MealCard';
import { mealPlan } from '../data/meal_plan';
import { formatDate } from '../utils/formatDate';


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
                <Modal show={alertShow} bg="warning">
                    <Modal.Header>
                        <Modal.Title>{'Alert!'}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <h5>{'Have you finished editing this meal plan?'}</h5>
                        <p>{'You will have to update pantry and shopping list manually\
                            if you make changes to this meal plan after clicking Yes.'}</p>
                    </Modal.Body>
                    <Modal.Footer className="d-flex justify-content-end">
                        <Button
                            onClick={() => setAlertShow(false)}
                            variant="success"
                        >
                            {'Yes'}
                        </Button>
                        <Button
                            onClick={() => setAlertShow(false)}
                            variant="danger"
                        >
                            {'No'}
                        </Button>
                    </Modal.Footer>
                </Modal>
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
