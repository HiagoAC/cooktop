import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { PantryIngredient, pantryIngredients} from '../data/pantry';
import { ItemCard } from '../components/ItemCard';
import { PantryIngredientModal } from '../components/PantryIngredientModal';
import styles from '../styles/Pantry.module.css';


export function Pantry() {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    return (
        <Container className="pb-4">
            <div className={`${styles.page_title} mt-3`}>Pantry</div>
            <div className="d-flex justify-content-center mt-2 mb-5">
                <Button
                    className={`${styles.custom_button}`}
                    onClick={handleModalShow}
                >
                    Add New Item
                </Button>
                <PantryIngredientModal
                    show={modalShow}
                    title="Add a new item"
                    buttonText="Save"
                    handleClose={handleModalClose}
                    handleClick={handleModalClose}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {pantryIngredients.map((ingredient: PantryIngredient) => (
                        <ItemCard key={ingredient.id} item={ingredient} />
                    ))}
                </div>
            </div>
        </Container>
    )
}
