import { v4 as uuid } from 'uuid';
import { Button, Card, Col, Form, ListGroup, Row } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { Ingredient } from '../types/interfaces';
import trashBinIcon from '../assets/trash_bin_icon.svg';
import styles from '../styles/IngredientsFormGroup.module.css';


interface Props {
    ingredients: (Ingredient | Omit<Ingredient, 'id'>)[];
    setIngredients: React.Dispatch<React.SetStateAction<(Ingredient | Omit<Ingredient, 'id'>)[]>>;
}

export function IngredientsFormGroup({ingredients, setIngredients}: Props) {
    const handleDelete = (name: string): void => {
        setIngredients((prevIngredients) =>
            prevIngredients.filter((ingredient) => ingredient.name !== name));
        };

    const addIngredient = (ingredient: Omit<Ingredient, "id">): void => {
        setIngredients((prevIngredients) => [...prevIngredients, ingredient]);
    };

    return (
        <Form.Group className="mb-3" controlId="ingredients">
            <Form.Label>Ingredients</Form.Label>
            <Card className={`mb-2 ${styles.ingredients_card}`}>
                <ListGroup variant="flush">
                    {ingredients.map(ingredient => (
                        <ListGroup.Item key={uuid()}>
                            <Row>
                                <Col>
                                    <div>{ingredient.name} - {ingredient.quantity} {ingredient.unit}</div>
                                </Col>
                                <Col className="d-flex justify-content-end">
                                    <Button
                                        className={styles.icon_button}
                                        onClick={() => handleDelete(ingredient.name)}
                                    >
                                        <img
                                            src={trashBinIcon}
                                            alt="delete"
                                            className={styles.icon}
                                        />
                                    </Button>
                                </Col>
                            </Row>
                        </ListGroup.Item>
                    ))}
                </ListGroup>
            </Card>
            <IngredientInputFields withAddButton={true} handleAdd={addIngredient} mode='create'/>
        </Form.Group>
    )
}
