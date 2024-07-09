import { useEffect, useState } from 'react';
import { Button, Container } from 'react-bootstrap';
import { ItemCard } from '../components/ItemCard';
import { ShoppingItemModal } from '../components/ShoppingItemModal';
import styles from '../styles/ShoppingList.module.css';
import { addItemToList, getShoppingList } from '../api/shoppingListApi';
import { ShoppingListItem } from '../types/interfaces';


export function ShoppingList() {
    const [modalShow, setModalShow] = useState(false);
    const [shoppingList, setShoppingList] = useState<ShoppingListItem[]>([]);

    const handleModalClose = () => setModalShow(false);
    const handleModalShow = () => setModalShow(true);

    const loadShoppingList = () => {
        getShoppingList().then(res => {
            console.log(res)
            if (res.status == 200) {
                setShoppingList(res.data);
            }
        });
    };

    const addItem = (shoppingItem: ShoppingListItem) => {
        if (!shoppingItem) {
            return;
        }
        addItemToList(shoppingItem).then(res => {
            console.log(res);
            handleModalClose();
        });
    };

    useEffect (() => {
        loadShoppingList();
    }, []);

    return (
        <Container className="pb-4">
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
                    title={"Add a new item"}
                    buttonText={"Save"}
                    handleClick={addItem}
                    handleClose={handleModalClose}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {shoppingList.map((item: ShoppingListItem) => (
                        <ItemCard key={item.name} item={item} cardType={"SHOPPING"}/>
                    ))}
                </div>
            </div>
        </Container>
    )
}
