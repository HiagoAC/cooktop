import { useEffect, useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { MealCard } from '../components/MealCard';
import type { MealPlan } from '../types/interfaces'
import { formatDate } from '../utils/formatDate';
import { UpdateListsFromMealPlanModal } from '../components/UpdateListsFromMealPlanModal';
import { CreateMealPlanModal } from '../components/CreateMealPlanModal';
import { getMealPlan } from '../api/mealPlansApi';


export function MealPlan() {

    const [updateAlertShow, setUpdateAlertShow] = useState<boolean>(false);
    const [newPlanAlertShow, setNewPlanAlertShow] = useState<boolean>(false);
    const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
    const [creationDate, setCreationDate] = useState<string>('');
    const [endDate, setEndDate] = useState<string>('');


    const loadMealPlan = () => {
        getMealPlan().then(res => {
            console.log(res)
            if (res.status == 200) {
                setMealPlan(res.data);
            }
        });
    };

    useEffect(() => {
        if (!mealPlan) return;
        const creationDateObject = new Date(mealPlan.creation_date);
        setCreationDate(formatDate(creationDateObject));
        const endDateObject = new Date(mealPlan.creation_date);
        endDateObject.setDate(endDateObject.getDate() + 7);
        setEndDate(formatDate(endDateObject));
    }, [mealPlan])

    useEffect(() => {
        loadMealPlan();
    }, []);

    return (
        <Container className="pb-4">
            <div className="page_title mt-3">
                { mealPlan ?
                    `Meal Plan for ${creationDate} to ${endDate}`
                    :
                    'No meal plan available :('
                }
            </div>
            <div className="d-flex justify-content-center mt-2 mb-5 gap-4">
                <Button
                    className="custom_button"
                    onClick={() => setNewPlanAlertShow(true)}
                >
                    {'Make New Plan'}
                </Button>
                <Button
                    className="custom_button"
                    onClick={() => setUpdateAlertShow(true)}
                >
                    {'Update Pantry & Shopping List'}
                </Button>
                <UpdateListsFromMealPlanModal
                    show={updateAlertShow}
                    onHide={() => setUpdateAlertShow(false)}
                />
                <CreateMealPlanModal
                    show={newPlanAlertShow}
                    onHide={() => setNewPlanAlertShow(false)}
                    refresh={() => loadMealPlan}
                />
            </div>
            <div>
                {mealPlan && Object.keys(mealPlan.meals).map((day: string) => (
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
