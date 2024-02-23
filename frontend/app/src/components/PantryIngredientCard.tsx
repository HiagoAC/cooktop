import { Button, Card, Col, Row } from 'react-bootstrap';
import { PantryIngredient } from '../data/pantry';
import editIcon from '../assets/edit_icon.svg';
import trashBinIcon from '../assets/trash_bin_icon.svg';
import styles from '../styles/PantryIngredientCard.module.css';


interface Props {
    ingredient: PantryIngredient
}

export function PantryIngredientCard({ingredient}: Props) {
    return (
        <Card body className={`mb-2 ${styles.card}`}>
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
                    <Button className={`${styles.icon_button}`}>
                        <img
                            src={editIcon}
                            alt="edit"
                            className={`${styles.icon}`}
                        />
                    </Button>
                    <Button className={`${styles.icon_button}`}>
                        <img
                            src={trashBinIcon}
                            alt="delete"
                            className={`${styles.icon}`}
                        />
                    </Button>
                </Col>
            </Row>
        </Card>
    )
}
