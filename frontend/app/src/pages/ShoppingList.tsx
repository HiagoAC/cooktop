import { useEffect, useState } from 'react';
import { Button, Container, Modal } from 'react-bootstrap';
import { ItemCard } from '../components/ItemCard';
import { ShoppingItemModal } from '../components/ShoppingItemModal';
import styles from '../styles/ShoppingList.module.css';
import {
    addItemToList,
    getShoppingList,
    updateShoppingItem,
    deleteShoppingItem
} from '../api/shoppingListApi';
import { ShoppingListItem } from '../types/interfaces';
import { createShoppingItemSchema, updateShoppingItemSchema } from '../api/apiSchemas/shoppingListSchemas';


export function ShoppingList() {
    const [addModalShow, setAddModalShow] = useState(false);
    const [clearModalShow, setClearModalShow] = useState(false);
    const [shoppingList, setShoppingList] = useState<ShoppingListItem[]>([]);

    const loadShoppingList = () => {
        getShoppingList().then(res => {
            console.log(res)
            if (res.status == 200) {
                setShoppingList(res.data);
            }
        });
    };

    const addItem = (shoppingItem: createShoppingItemSchema) => {
        if (!shoppingItem) {
            return;
        }
        addItemToList(shoppingItem).then(res => {
            console.log(res);
            loadShoppingList();
        });
    };

    const updateItem = (shoppingItem: updateShoppingItemSchema | Omit<updateShoppingItemSchema, 'id'>) => {
        if (!shoppingItem || !('id' in shoppingItem)) {
            return;
        }
        updateShoppingItem(shoppingItem).then(res => {
            console.log(res);
            loadShoppingList();
        });
    };

    const deleteItem = (id: number) => {
        deleteShoppingItem(id).then(res => {
            console.log(res);
            loadShoppingList();
        });
    };

    const clearList = async () => {
        // Add prompt to add items to pantry
        await Promise.all(
            shoppingList.map(item =>
                deleteShoppingItem(item.id).then(
                    res => console.log(res))));
        loadShoppingList();
        setClearModalShow(false);
    }

    useEffect (() => {
        loadShoppingList();
    }, []);

    return (
        <Container className="pb-4">
            <div className={`${styles.page_title} mt-3`}>Shopping List</div>
            <div className="d-flex justify-content-center mt-2 mb-5 gap-4">
                <Button
                    className={`${styles.custom_button}`}
                    onClick={() => setAddModalShow(true)}
                >
                    Add New Item
                </Button>
                <Button
                    className={`${styles.custom_button}`}
                    onClick={() => setClearModalShow(true)}
                >
                    Clear List
                </Button>
                <Modal
                    show={clearModalShow}
                    onHide={() => setClearModalShow(false)}
                >
                    <Modal.Header>
                        <Modal.Title>Clear List</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <p>{'Are you sure you want to clear your shopping list?'}</p>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="danger"
                            onClick={() => {setClearModalShow(false)}}
                        >
                            Close
                        </Button>
                        <Button variant="success" onClick={clearList}>
                            Clear List
                        </Button>
                    </Modal.Footer>
                </Modal>
                <ShoppingItemModal
                    show={addModalShow}
                    title={"Add a new item"}
                    mode="create"
                    buttonText={"Save"}
                    handleClick={addItem}
                    handleClose={() => setAddModalShow(false)}
                />
            </div>
            <div className="d-flex justify-content-center">
                <div className={`${styles.ingredient_list_container}`}>
                    {shoppingList.map((item: ShoppingListItem) => (
                        <ItemCard
                            key={item.name}
                            item={item}
                            cardType={"SHOPPING"}
                            handleEdit={updateItem}
                            handleDelete={deleteItem}
                        />
                    ))}
                </div>
            </div>
        </Container>
    )
}
