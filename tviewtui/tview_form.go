// Demo code for the Form primitive.
package tviewtui

import (
	"fmt"
	"github.com/rivo/tview"
	"strconv"
)

func GetValues() []float64 {
	values := make([]float64, 6)
	app := tview.NewApplication()
	form := tview.NewForm().
		//AddDropDown("Title", []string{"Mr.", "Ms.", "Mrs.", "Dr.", "Prof."}, 0, nil).
		AddInputField("clogP", "", 5, nil, nil).
		AddInputField("clogD", "", 5, nil, nil).
		AddInputField("MW", "", 5, nil, nil).
		AddInputField("pKa", "", 5, nil, nil).
		AddInputField("TPSA", "", 5, nil, nil).
		AddInputField("HBD", "", 5, nil, nil).
		AddButton("Close", func() {
			app.Stop()
		})
	form.SetBorder(true).SetTitle("Enter some data").SetTitleAlign(tview.AlignLeft)
	if err := app.SetRoot(form, true).EnableMouse(true).EnablePaste(true).Run(); err != nil {
		panic(err)
	}
	//i, s := form.GetFormItem(0).(*tview.DropDown).GetCurrentOption()
	//fmt.Printf("%d %s\n", i, s)
	clogp, err := strconv.ParseFloat(form.GetFormItem(0).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[0] = clogp
	clogd, err := strconv.ParseFloat(form.GetFormItem(1).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[1] = clogd
	mw, err := strconv.ParseFloat(form.GetFormItem(2).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[2] = mw
	pka, err := strconv.ParseFloat(form.GetFormItem(3).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[3] = pka
	tpsa, err := strconv.ParseFloat(form.GetFormItem(4).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[4] = tpsa
	hbd, err := strconv.ParseFloat(form.GetFormItem(5).(*tview.InputField).GetText(), 64)
	if err != nil {
		fmt.Println("Error", err)
		return nil
	}
	values[5] = hbd
	return values
}
