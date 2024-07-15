import { useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { pantryIngredients} from '../data/pantry';
import { PantryIngredient } from '../types/interfaces';
import { ItemCard } from '../components/ItemCard';
import { PantryIngredientModal } from '../components/PantryIngredientModal';
import { addItemToPantry } from '../api/pantryApi';
import { createPantryItemSchema } from '../api/apiSchemas/pantrySchemas';
import styles from '../styles/Pantry.module.css';


export function Pantry() {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    const addItem = (pantryItem: Omit<PantryIngredient, 'id'>) => {
        console.log('Got here ...')
        if (!pantryItem) {
            console.log('but...')
            return;
        }
        addItemToPantry({...pantryItem}).then(res => {
            console.log(res);
            handleModalClose();
        });
    }

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
                    mode={'create'}
                    title="Add a new item"
                    buttonText="Save"
                    handleClick={addItem}
                    handleClose={handleModalClose}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {pantryIngredients.map((ingredient: PantryIngredient) => (
                        <ItemCard key={ingredient.name} item={ingredient} cardType={"PANTRY"}/>
                    ))}
                </div>
            </div>
        </Container>
    )
}