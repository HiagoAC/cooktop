import { useEffect, useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { PantryIngredient } from '../types/interfaces';
import { ItemCard } from '../components/ItemCard';
import { PantryIngredientModal } from '../components/PantryIngredientModal';
import {
    addItemToPantry,
    getPantry,
    updatePantryItem,
    deletePantryItem
} from '../api/pantryApi';
import styles from '../styles/Pantry.module.css';


export function Pantry() {
    const [modalShow, setModalShow] = useState<boolean>(false);
    const [pantryIngredients, setPantry] = useState<PantryIngredient[]>([]);

    const loadPantry = () => {
        getPantry().then(res => {
            console.log(res)
            if (res.status == 200) {
                setPantry(res.data);
            }
        });
    };

    const addItem = (pantryItem: Omit<PantryIngredient, 'id'>) => {
        if (!pantryItem) {
            return;
        }
        addItemToPantry({...pantryItem}).then(res => {
            console.log(res);
            loadPantry();
        });
    };

    const updateItem = (pantryItem: PantryIngredient) => {
        if (!pantryItem) {
            return;
        }
        updatePantryItem({...pantryItem}).then(res => {
            console.log(res);
            loadPantry();
        });
    };

    const deleteItem = (id: number) => {
        deletePantryItem(id).then(res => {
            console.log(res);
            loadPantry();
        });
    };

    useEffect (() => {
        loadPantry();
    }, []);

    return (
        <Container className="pb-4">
            <div className={`${styles.page_title} mt-3`}>Pantry</div>
            <div className="d-flex justify-content-center mt-2 mb-5">
                <Button
                    className={`${styles.custom_button}`}
                    onClick={() => setModalShow(true)}
                >
                    Add New Item
                </Button>
                <PantryIngredientModal
                    show={modalShow}
                    mode={'create'}
                    title="Add a new item"
                    buttonText="Save"
                    handleClick={addItem}
                    handleClose={() => setModalShow(false)}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {pantryIngredients.map((ingredient: PantryIngredient) => (
                        <ItemCard
                            key={ingredient.name}
                            item={ingredient}
                            cardType={"PANTRY"}
                            handleEdit={updateItem}
                            handleDelete={deleteItem}
                        />
                    ))}
                </div>
            </div>
        </Container>
    )
}
