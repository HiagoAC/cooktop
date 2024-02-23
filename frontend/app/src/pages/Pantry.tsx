import { useState } from 'react';
import { Button } from 'react-bootstrap';
import { PantryIngredient, pantryIngredients} from '../data/pantry';
import { PantryIngredientCard } from '../components/PantryIngredientCard';
import { PantryIngredientModal } from '../components/PantryIngredientModal';
import styles from '../styles/Pantry.module.css';


export function Pantry() {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);
    return (
        <>
            <div className="page_title mt-3">Pantry</div>
            <div className="d-flex justify-content-center mt-2 mb-5">
                <Button
                    className={`${styles.custom_button}`}
                    onClick={handleModalShow}
                >
                    Add new item
                </Button>
                <PantryIngredientModal
                    show={modalShow}
                    title="Add a new ingredient"
                    buttonText="Save"
                    handleClose={handleModalClose}
                    handleClick={handleModalClose}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_card_container}`}>
                    {pantryIngredients.map((ingredient: PantryIngredient) => (
                        <PantryIngredientCard key={ingredient.id} ingredient={ingredient} />
                    ))}
                </div>
            </div>
        </>
    )
}
