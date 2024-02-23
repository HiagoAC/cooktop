import { Button, Card, Col, Row } from 'react-bootstrap';
import { PantryIngredient } from '../data/pantry';
import editIcon from '../assets/edit_icon.svg';
import trashBinIcon from '../assets/trash_bin_icon.svg';
import '../styles/PantryIngredientCard.css';


interface Props {
    ingredient: PantryIngredient
}

export function PantryIngredientCard({ingredient}: Props) {
    return (
        <Card body className="mb-2 card">
            <Row>
                <Col>
                    <div>
                        {ingredient.name}: {ingredient.quantity} {ingredient.unit}
                    </div>
                    <div>
                        {
                            ingredient.expiration?
                            `expires in: ${ingredient.expiration}`
                            : null
                        }
                    </div>
                </Col>
                <Col className="d-flex justify-content-end">
                    <Button className="edit-button">
                        <img
                            src={editIcon}
                            alt="edit"
                            className="edit-icon"
                        />
                    </Button>
                    <Button className="edit-button">
                        <img
                            src={trashBinIcon}
                            alt="delete"
                            className="edit-icon"
                        />
                    </Button>
                </Col>
            </Row>
        </Card>
    )
}
