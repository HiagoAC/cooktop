import { useState } from 'react';
import { Button, Card, Col, Row } from 'react-bootstrap';
import { PantryIngredientModal } from './PantryIngredientModal';
import { PantryIngredient } from '../types/interfaces';
import { ShoppingListItem } from '../types/interfaces';
import editIcon from '../assets/edit_icon.svg';
import trashBinIcon from '../assets/trash_bin_icon.svg';
import styles from '../styles/PantryIngredientCard.module.css';
import { ShoppingItemModal } from './ShoppingItemModal';

type CardType = "PANTRY" | "SHOPPING";
type CardItem = PantryIngredient | ShoppingListItem;

interface Props {
    item: CardItem;
    cardType: CardType;
    handleEdit: (cardItem: CardItem | Omit<CardItem, 'id'>) => void;
    handleDelete: (id: number) => void;
}

export function ItemCard({item, cardType, handleEdit, handleDelete}: Props) {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    return (
        <Card body className={`mb-2 ${styles.card}`}>
            <Row>
                <Col>
                    <div className="fs-5">
                        {item.name}: {item.quantity} {item.unit}
                    </div>
                    <div className="fs-6">
                        {
                            'expiration' in item && item.expiration?
                            `expires in: ${item.expiration}`
                            : null
                        }
                    </div>
                </Col>
                <Col className="d-flex justify-content-end">
                    <Button
                        className={`${styles.icon_button}`}
                        onClick={handleModalShow}
                    >
                        <img
                            src={editIcon}
                            alt="edit"
                            className={`${styles.icon}`}
                        />
                    </Button>
                    {  cardType === "PANTRY" ?
                        (<PantryIngredientModal
                            show={modalShow}
                            title="Edit pantry entry"
                            buttonText="Save"
                            mode = "edit"
                            handleClose={handleModalClose}
                            handleClick={handleEdit}
                            pantryIngredientInit={item as PantryIngredient}
                        />) : cardType === "SHOPPING" ? (
                            <ShoppingItemModal
                                show={modalShow}
                                title="Edit shopping list item"
                                buttonText="Save"
                                mode = "edit"
                                handleClose={handleModalClose}
                                handleClick={handleEdit}
                                shoppingListItem={item as ShoppingListItem}
                            /> 
                        ) : (null)
                    }
                    <Button
                        className={`${styles.icon_button}`}
                        onClick={() => {handleDelete(item.id)}}
                    >
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
