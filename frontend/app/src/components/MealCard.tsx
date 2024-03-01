import { useState } from 'react';
import { Button, Card, Col, Form, Row } from 'react-bootstrap';
import { EditMealModal } from './EditMealModal';
import { Meal } from '../data/meal_plan';
import { RecipeInList } from './RecipeInList';
import editIcon from '../assets/edit_icon.svg';
import styles from '../styles/PantryIngredientCard.module.css';


interface Props {
    day: number;
    meal: Meal;
}

export function MealCard({day, meal}: Props) {
    const [editModalShow, setEditModalShow] = useState(false);

    const handleEditModalClose = () => setEditModalShow(false);
    const handleEditModalShow = () => setEditModalShow(true);

    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <Row>
                        <Col>
                            <Form>
                                <Form.Check
                                    type='checkbox'
                                    label={`Day ${day}:`}
                                />
                            </Form>
                        </Col>
                        <Col className="d-flex justify-content-end">
                            <Button
                                className={`${styles.icon_button}`}
                                onClick={handleEditModalShow}
                            >
                                <img
                                    src={editIcon}
                                    alt="edit"
                                    className={`${styles.icon}`}
                                />
                            </Button>
                            <EditMealModal
                                recipes={{
                                    'mainDish': meal.main_dish,
                                    'sideDish': meal.side_dish,
                                    'salad': meal.salad
                                }}
                                show={editModalShow}
                                handleClose={handleEditModalClose}
                            />
                        </Col>
                    </Row>
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row lg={3} md={2} xs={1} className="g-4">
                    <Col>
                        <RecipeInList {...meal.main_dish}/>
                    </Col>
                    <Col>
                        <RecipeInList {...meal.side_dish}/>
                    </Col>
                    <Col>
                        <RecipeInList {...meal.salad}/>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}
