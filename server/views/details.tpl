% rebase('base.tpl', title="Experiment Details")

<h1>Passage Parse</h1>

<table class="table table-hover">

    <a href="/passage/{{experiment.id}}/add">Add sentence</a>

    <tbody>
        % for row in experiment.sentences:
        <tr>
            <td>
                <a class="btn btn-outline-success btn-sm" href="/sentences/{{row.id}}">Show</a> {{ row.text }}
            </td>
        </tr>
        %end
    </tbody>
</table>