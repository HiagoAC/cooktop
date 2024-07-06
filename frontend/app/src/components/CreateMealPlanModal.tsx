import { Modal, Button, Form } from 'react-bootstrap';
import { useState } from 'react';
import { createMealPlan } from '../api/mealPlansApi';
import { BadgeStackFormGroup } from './BadgeStackFormGroup';

interface Props {
    show: boolean;
    onHide: () => void;
    refresh: () => void;
}


export function CreateMealPlanModal({ show, onHide, refresh }: Props) {
    const [ingredients, setIngredients] = useState<string[]>([]);

    const handleCreateMealPlan = async () => {
        createMealPlan({requested_ingredients: ingredients}).then(res => {
            if (res.status == 201) {
                refresh();
            }
        });
        onHide();
    };

    return (
        <Modal show={show} onHide={onHide} bg="warning">
            <Modal.Header>
                <Modal.Title>{'Alert!'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h5>{'Making a new plan will replace your current plan.'}</h5>
                <Form>
                    <BadgeStackFormGroup
                        items={ingredients}
                        setItems={setIngredients}
                        label="What ingredients do you want to use?"
                        placeholder="Type a new ingredient and press add."
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-end">
                <Button
                    onClick={handleCreateMealPlan}
                    variant="success"
                >
                    {'Make new plan'}
                </Button>
                <Button
                    onClick={onHide}
                    variant="danger"
                >
                    {'Go back'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
