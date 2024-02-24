import { useState } from 'react';
import { Button } from 'react-bootstrap';
import { ItemCard } from '../components/ItemCard';
import { ShoppingItemModal } from '../components/ShoppingItemModal';
import { ShoppingItem, shoppingList} from '../data/shopping_list';
import styles from '../styles/ShoppingList.module.css';


export function ShoppingList() {
    const [modalShow, setModalShow] = useState(false);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    return (
        <>
            <div className={`${styles.page_title} mt-3`}>Shopping List</div>
            <div className="d-flex justify-content-center mt-2 mb-5 gap-4">
                <Button
                    className={`${styles.custom_button}`}
                    onClick={handleModalShow}
                >
                    Add New Item
                </Button>
                <Button className={`${styles.custom_button}`}>
                    Clear List
                </Button>
                <ShoppingItemModal
                    show={modalShow}
                    title="Add a new item"
                    buttonText="Save"
                    handleClose={handleModalClose}
                    handleClick={handleModalClose}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {shoppingList.map((item: ShoppingItem) => (
                        <ItemCard key={item.id} item={item} />
                    ))}
                </div>
            </div>
        </>
    )
}
