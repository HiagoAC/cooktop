import { Card, Col, Form, Row } from 'react-bootstrap';
import { Meal } from '../data/meal_plan';
import { RecipeInList } from './RecipeInList';


interface Props {
    day: number;
    meal: Meal;
}

export function MealCard({day, meal}: Props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <Form>
                        <Form.Check
                            type='checkbox'
                            label={`Day ${day}:`}
                        />
                    </Form>
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
