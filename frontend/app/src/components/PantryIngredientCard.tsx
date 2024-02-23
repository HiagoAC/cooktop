import { useState } from 'react';
import { Button, Card, Col, Row } from 'react-bootstrap';
import { PantryIngredientModal } from './PantryIngredientModal';
import { PantryIngredient } from '../data/pantry';
import editIcon from '../assets/edit_icon.svg';
import trashBinIcon from '../assets/trash_bin_icon.svg';
import styles from '../styles/PantryIngredientCard.module.css';


interface Props {
    ingredient: PantryIngredient
}

export function PantryIngredientCard({ingredient}: Props) {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    return (
        <Card body className={`mb-2 ${styles.card}`}>
            <Row>
                <Col>
                    <div className="fs-5">
                        {ingredient.name}: {ingredient.quantity} {ingredient.unit}
                    </div>
                    <div className="fs-6">
                        {
                            ingredient.expiration?
                            `expires in: ${ingredient.expiration}`
                            : null
                        }
                    </div>
                </Col>
                <Col className="d-flex justify-content-end">
                    <Button className={`${styles.icon_button}`} onClick={handleModalShow}>
                        <img
                            src={editIcon}
                            alt="edit"
                            className={`${styles.icon}`}
                        />
                    </Button>
                    <PantryIngredientModal
                            show={modalShow}
                            title="Edit pantry entry"
                            buttonText="Save"
                            handleClose={handleModalClose}
                            handleClick={handleModalClose}
                        />
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
